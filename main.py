from chat import Chat
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="LLM-Test")
    parser.add_argument(dest="input", help="输入文件的路径")
    parser.add_argument("-o","--outfile", dest="output", help="输出文件的路径")
    parser.add_argument("-b","--base_url", dest="base_url", help="OpenAI base url")
    parser.add_argument("-k", "--api_key", dest="api_key", help="OpenAI API key")
    parser.add_argument("-m", "--model_name", dest="model_name", help="Model name")
    args = parser.parse_args()
    with open(args.input, "r") as f:
        dataset = json.load(f)

    outputs = []
    for data in dataset:
        chat = Chat(base_url=args.base_url, api_key=args.api_key, model=args.model_name, history=data.get("history", []))
        output = chat.chat(data["instruction"], data.get("input", ""))
        outputs.append(output)

if __name__ == "__main__":
    main()