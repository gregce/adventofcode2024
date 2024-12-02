from openai import OpenAI
from app.config import Config
import os
from dotenv import load_dotenv
import io
import logging

logger = logging.getLogger(__name__)

class LLMHandler:
    AVAILABLE_MODELS = {
        'gpt-4-turbo-preview': 'GPT-4 Turbo',
        'gpt-4': 'GPT-4',
        'gpt-3.5-turbo': 'GPT-3.5 Turbo'
    }

    MODEL_PRICING = {
        'gpt-4-turbo-preview': {'input': 0.01, 'output': 0.03},
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015}
    }

    def calculate_cost(self, model, input_tokens, output_tokens):
        pricing = self.MODEL_PRICING[model]
        input_cost = (input_tokens / 1000) * pricing['input']
        output_cost = (output_tokens / 1000) * pricing['output']
        total_cost = input_cost + output_cost
        return round(total_cost, 6)

    def __init__(self):
        self.client = None
        self.setup_client()
    
    def setup_client(self):
        api_key = Config.get_openai_key()
        if not api_key:
            raise ValueError("OpenAI API key not found. Please provide an API key.")
        self.client = OpenAI(api_key=api_key)
    
    def validate_api_key(self, api_key):
        try:
            test_client = OpenAI(api_key=api_key)
            # Try a simple API call to validate the key
            test_client.models.list()
            return True
        except Exception as e:
            logger.error(f"API key validation failed: {str(e)}")
            return False
    
    def generate_spec(self, instructions, model='gpt-4-turbo-preview', input_file=None):
        try:
            logger.info(f"Generating spec using model: {model}")
            file_content = None
            if input_file and hasattr(input_file, 'read'):
                if isinstance(input_file, io.BytesIO):
                    file_content = input_file.read().decode('utf-8')
                else:
                    file_content = input_file.read()
                if isinstance(file_content, bytes):
                    file_content = file_content.decode('utf-8')
                logger.info("Successfully processed input file")
            
            system_prompt = """You are a solution architect for Advent of Code problems.
            Generate a detailed specification based on the given instructions and input data.
            The specification should include:
            1. Problem Analysis: Break down the problem requirements
            2. Input Processing: How the input data should be parsed
            3. Solution Strategy: Step-by-step approach to solve the problem
            4. Expected Output: What the solution should return
            5. Edge Cases: Any special cases to handle
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""Instructions: {instructions}
                
                Input Data Sample:
                {file_content if file_content else 'No input file provided'}
                
                Please provide a detailed specification following the format above."""}
            ]
            
            logger.info("Sending request to OpenAI API for spec generation...")
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Calculate and log token usage
            usage = response.usage
            cost = self.calculate_cost(model, usage.prompt_tokens, usage.completion_tokens)
            
            usage_info = {
                'input_tokens': usage.prompt_tokens,
                'output_tokens': usage.completion_tokens,
                'total_tokens': usage.total_tokens,
                'cost': cost
            }
            
            logger.info(f"Token usage for spec: {usage_info}")
            logger.info("Received specification from OpenAI API")
            
            return response.choices[0].message.content, usage_info
        except Exception as e:
            logger.error(f"Error in generate_spec: {str(e)}")
            raise Exception(f"Error generating spec: {str(e)}")
    
    def generate_solution(self, spec, model='gpt-4-turbo-preview'):
        try:
            logger.info(f"Generating solution using model: {model}")
            
            system_prompt = """You are a Python developer implementing Advent of Code solutions.
            Generate ONLY the Python code solution, without any explanations or markdown.
            The solution must:
            1. Start with necessary imports (including sys for command line args)
            2. Read input from sys.argv[1] if provided, otherwise default to 'input.txt'
            3. Include a main function
            4. Print the final result
            5. Include proper error handling for file operations
            
            Example structure:
            ```python
            import sys
            
            def main():
                input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
                try:
                    with open(input_file) as f:
                        # process input
                        # compute result
                        print(result)
                except FileNotFoundError:
                    print(f"Error: Could not find input file {input_file}")
                    sys.exit(1)
                except Exception as e:
                    print(f"Error: {str(e)}")
                    sys.exit(1)
            
            if __name__ == "__main__":
                main()
            ```
            
            DO NOT include any explanatory text - ONLY PYTHON CODE."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a Python solution for this specification:\n{spec}"}
            ]
            
            logger.info("Sending request to OpenAI API for solution generation...")
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Calculate and log token usage
            usage = response.usage
            cost = self.calculate_cost(model, usage.prompt_tokens, usage.completion_tokens)
            
            usage_info = {
                'input_tokens': usage.prompt_tokens,
                'output_tokens': usage.completion_tokens,
                'total_tokens': usage.total_tokens,
                'cost': cost
            }
            
            logger.info(f"Token usage for solution: {usage_info}")
            logger.info("Received solution from OpenAI API")
            
            # Clean up the response to ensure it's only Python code
            solution = response.choices[0].message.content.strip()
            if not solution.startswith('def') and not solution.startswith('import') and not solution.startswith('#'):
                import re
                code_blocks = re.findall(r'```python\n(.*?)\n```', solution, re.DOTALL)
                if code_blocks:
                    solution = code_blocks[0].strip()
                else:
                    lines = solution.split('\n')
                    code_lines = []
                    started = False
                    for line in lines:
                        if started or line.startswith('def') or line.startswith('import') or line.startswith('#'):
                            started = True
                            code_lines.append(line)
                    solution = '\n'.join(code_lines)
            
            if not solution:
                raise Exception("Failed to generate valid Python code")
            
            return solution, usage_info
            
        except Exception as e:
            logger.error(f"Error in generate_solution: {str(e)}")
            raise Exception(f"Error generating solution: {str(e)}")