import argparse
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from pathlib import Path
import json
import jieba
from pypinyin import lazy_pinyin, Style

def convert_char_to_pinyin(text_list, polyphone=True):
    if jieba.dt.initialized is False:
        jieba.default_logger.setLevel(50)  # CRITICAL
        jieba.initialize()

    final_text_list = []
    custom_trans = str.maketrans(
        {";": ",", "“": '"', "”": '"', "‘": "'", "’": "'"}
    )  # add custom trans here, to address oov

    def is_chinese(c):
        return (
            "\u3100" <= c <= "\u9fff"  # common chinese characters
        )

    for text in text_list:
        char_list = []
        text = text.translate(custom_trans)
        for seg in jieba.cut(text):
            seg_byte_len = len(bytes(seg, "UTF-8"))
            if seg_byte_len == len(seg):  # if pure alphabets and symbols
                if char_list and seg_byte_len > 1 and char_list[-1] not in " :'\"":
                    char_list.append(" ")
                char_list.extend(seg)
            elif polyphone and seg_byte_len == 3 * len(seg):  # if pure east asian characters
                seg_ = lazy_pinyin(seg, style=Style.TONE3, tone_sandhi=True)
                for i, c in enumerate(seg):
                    if is_chinese(c):
                        char_list.append(" ")
                    char_list.append(seg_[i])
            else:  # if mixed characters, alphabets and symbols
                for c in seg:
                    if ord(c) < 256:
                        char_list.extend(c)
                    elif is_chinese(c):
                        char_list.append(" ")
                        char_list.extend(lazy_pinyin(c, style=Style.TONE3, tone_sandhi=True))
                    else:
                        char_list.append(c)
        final_text_list.append(char_list)

    return final_text_list

def deal_with_jsonl(jsonl_path, dnsmosThreshold, polyphone):
    vocab_set = set()
    results = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            obj = json.loads(line)
            lang = obj["language"]
            text = obj["text"]
            dnsmos = obj["dnsmos"]
            if dnsmos < dnsmosThreshold:
                continue
            if lang == "zh":
                text = text.translate(
                    str.maketrans({",": "，", "!": "！", "?": "？"})
                )
            tokens = convert_char_to_pinyin([text], polyphone=polyphone)[0]
            vocab_set.update(tokens)
            results.append(obj)
    
    output_jsonl_path = jsonl_path.parent.parent.parent / f"{jsonl_path.parent.parent.name}_filter" / jsonl_path.parent.name /jsonl_path.name
    output_jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_jsonl_path, "w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
    
    return vocab_set

def main(args):
    '''
    筛选音频数据集的metadata并输出筛选后的metadata，并创建字符级别分词的词汇表`vocab.txt`
    '''
    input_dir = Path(args.input_dir)
    polyphone = args.polyphone
    dnsmosThreshold = args.dnsmosThreshold
    langs = args.langs
    max_workers = args.max_workers
    
    futures = []
    total_vocab_set = set()
    
    with ProcessPoolExecutor(max_workers) as executor:
        for lang in langs:
            data_input_path = input_dir / lang
            for jsonl_path in data_input_path.iterdir():
                futures.append(executor.submit(deal_with_jsonl, jsonl_path, dnsmosThreshold, polyphone))
        
        # 收集结果
        for future in tqdm(futures, desc=f"Collecting result: "):
            vocab_set = future.result()
            total_vocab_set.update(vocab_set)            
    
    print(f"Total vocabulary size: {len(total_vocab_set)}")
    vocab_path = input_dir.parent / f"{input_dir.name}_filter" / "vocab.txt"
    with open(vocab_path, "w", encoding="utf-8") as f:
        for vocab in sorted(total_vocab_set):
            f.write(vocab + "\n")
    print(f"Vocabulary saved to: {vocab_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Metadata to vocab.txt")
    parser.add_argument(
        "-d", "--dnsmosThreshold", type=float, default=3.0,
        help="The minimum of dnsmos."
    )
    parser.add_argument(
        "-i", "--input_dir", type=str, required=True,
        help="The path of input dir."
    )
    parser.add_argument(
        "-l", "--langs", type=str, nargs="+", default=["ZH", "EN"],
        help="The language of the data to be processed."
    )
    parser.add_argument(
        "-p", "--polyphone", action="store_true",
        help="whether to process polyphone"
    )
    parser.add_argument(
        "-w", "--max_workers", type=int, default=4,
        help="input num of workers"
    )
    
    args = parser.parse_args()
    print(f"Processing with arguments: {args}")
    main(args)