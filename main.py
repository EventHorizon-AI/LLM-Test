import itertools
import tqdm
from chat import Chat
import argparse
import json

class TestChat(Chat):
    def __init__(self,args: dict):
        temperature_values = [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
        top_p_values = [0.8, 0.85, 0.9, 0.95, 1.0]

        self.param_combinations = list(itertools.product(temperature_values, top_p_values))
        self.args = args

    def test_parameter_combination(self, prompt,history = []) -> list:
        results = []
        for temp, p in tqdm.tqdm(self.param_combinations):
            chat = Chat(base_url=self.args.base_url, api_key=self.args.api_key, model=self.args.model_name, history=history)
            result = chat.chat(**prompt, temperature=temp, top_p=p)
            print(f"Temperature: {temp}, Top_P: {p} -> Result:\n{result}")
            results.append({"temperature": temp, "top_p": p, "result": result})
        
        return results

def main():
    parser = argparse.ArgumentParser(description="LLM-Test")
    parser.add_argument(dest="input", help="输入文件的路径")
    parser.add_argument("-o","--outfile", dest="output", help="输出文件的路径")
    parser.add_argument("-b","--base_url", dest="base_url", help="OpenAI base url")
    parser.add_argument("-k", "--api_key", dest="api_key", help="OpenAI API key")
    parser.add_argument("-m", "--model_name", dest="model_name", help="Model name")
    parser.add_argument("-n", "--num", dest="num", type=int, default=1, help="反复测试的次数")
    args = parser.parse_args()
    with open(args.input, "r", encoding='utf-8') as f:
        dataset = json.load(f)

    outputs = []
    for data in dataset:
        for _ in range(args.num):
            prompt = {
                "instruction": data["instruction"],
                "input": data.get("input", "")
            }
            test_chat = TestChat(args)
            output = test_chat.test_parameter_combination(prompt)

            outputs.append(output)

        with open(args.output, "w", encoding='utf-8') as f:
            json.dump(outputs, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()