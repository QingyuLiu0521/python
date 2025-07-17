# sample scripts
import argparse

def main(args):
    print(f"para1: {args.para1}")
    print(f"p2: {args.p2}")
    print(f"p3: {args.p3}")
    print(f"p4: {args.p4}")
    print(f"pn: {args.pn}")

if __name__ == '__main__':
    # 1. 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description='This is a sample script.')
    
    # 2. 添加参数
    parser.add_argument(
        "para1", type=str, default="a", 
        help="Input parameter1"
    )
    
    parser.add_argument(
        "-p", "--p2", type=int, default=1,
        help="Input parameter2"
    )
    
    parser.add_argument(
        "--p3", type=str, required=True,
        help="Input parameter3"
    )
    
    parser.add_argument(
        "--p4", action='store_true',
        help='Bool switch parameter'
    )
    
    parser.add_argument(
        "--pn", type=int, nargs='+',
        help="Input parametern"
    )
    
    # 3. 解析参数
    args = parser.parse_args()
    
    # 4. 将args传入main，在main中使用参数
    main(args)