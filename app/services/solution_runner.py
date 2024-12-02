import tempfile
import subprocess
import os
from pathlib import Path
import sys
import logging

logger = logging.getLogger(__name__)

class SolutionRunner:
    def run_solution(self, solution_code, input_file=None):
        temp_solution_path = None
        input_path = None
        
        try:
            # Create temporary directory that's accessible in container
            temp_dir = Path('/tmp/aoc_solutions')
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            # Create solution file
            temp_solution_path = temp_dir / f'solution_{os.getpid()}.py'
            with open(temp_solution_path, 'w') as temp_solution:
                if 'if __name__ == "__main__":' not in solution_code:
                    solution_code += '\n\nif __name__ == "__main__":\n    main()'
                temp_solution.write(solution_code)
            
            # Set up command
            cmd = [sys.executable, str(temp_solution_path)]  # Use sys.executable for correct Python path
            
            # Handle input file
            if input_file:
                input_path = temp_dir / f'input_{os.getpid()}.txt'
                input_file.seek(0)
                with open(input_path, 'wb') as temp_input:
                    temp_input.write(input_file.read())
                cmd.append(str(input_path))
            
            logger.info(f"Running solution with command: {' '.join(cmd)}")
            
            # Run with resource limits
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                timeout=30,  # Add timeout
                env={
                    **os.environ,
                    'PYTHONPATH': os.getcwd()  # Ensure proper Python path
                }
            )
            
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'exit_code': result.returncode,
                'code': solution_code
            }
            
        except subprocess.TimeoutExpired:
            logger.error("Solution execution timed out")
            return {
                'error': 'Solution execution timed out after 30 seconds',
                'exit_code': -1,
                'code': solution_code
            }
        except Exception as e:
            logger.error(f"Error running solution: {str(e)}")
            return {
                'error': str(e),
                'exit_code': -1,
                'code': solution_code
            }
        finally:
            # Clean up temporary files
            try:
                if temp_solution_path and temp_solution_path.exists():
                    temp_solution_path.unlink()
                if input_path and input_path.exists():
                    input_path.unlink()
            except Exception as e:
                logger.error(f"Error cleaning up temporary files: {str(e)}")