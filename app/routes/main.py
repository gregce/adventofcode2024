from flask import Blueprint, request, render_template, Response, session, redirect, url_for, jsonify
from app import llm, runner, logger
from app.services.llm_handler import LLMHandler
from app.config import Config
import json
import queue
import threading

main_bp = Blueprint('main', __name__)
status_updates = queue.Queue()

def add_status(message, error=False, type='info'):
    status_updates.put({
        'message': message,
        'error': error,
        'type': type,
        'complete': False
    })

@main_bp.route('/', methods=['GET'])
def index():
    has_api_key = bool(Config.get_openai_key())
    return render_template('index.html', 
                         models=LLMHandler.AVAILABLE_MODELS,
                         has_api_key=has_api_key)

@main_bp.route('/generate/status')
def status():
    def generate():
        while True:
            try:
                status = status_updates.get(timeout=30)
                yield f"data: {json.dumps(status)}\n\n"
                if status.get('complete'):
                    break
            except queue.Empty:
                break
    
    return Response(generate(), mimetype='text/event-stream')

@main_bp.route('/generate', methods=['POST'])
def generate():
    try:
        add_status(" New generation request received")
        total_cost = 0
        total_tokens = 0
        
        instructions = request.form.get('instructions')
        if not instructions:
            add_status("❌ No instructions provided", True, 'error')
            return "No instructions provided", 400
        
        model = request.form.get('model')
        if not model:
            add_status("❌ No model selected", True, 'error')
            return "No model selected", 400
        
        add_status(f"📝 Processing request with model: {model}")
        
        if request.files.get('file'):
            add_status(f"📁 Processing input file: {request.files['file'].filename}", type='file')
        
        try:
            # Generate spec
            add_status("🔄 Generating specification...", type='api')
            spec, spec_usage = llm.generate_spec(instructions, model=model, input_file=request.files.get('file'))
            add_status("✅ Specification generated successfully", type='success')
            add_status(
                f"📊 Spec tokens - Input: {spec_usage['input_tokens']}, "
                f"Output: {spec_usage['output_tokens']}, "
                f"Cost: ${spec_usage['cost']:.4f}",
                type='api'
            )
            total_cost += spec_usage['cost']
            total_tokens += spec_usage['total_tokens']
            status_updates.put({'spec': spec})
            
            # Generate solution
            add_status("🔄 Generating solution...", type='api')
            solution, solution_usage = llm.generate_solution(spec, model=model)
            add_status("✅ Solution generated successfully", type='success')
            add_status(
                f"📊 Solution tokens - Input: {solution_usage['input_tokens']}, "
                f"Output: {solution_usage['output_tokens']}, "
                f"Cost: ${solution_usage['cost']:.4f}",
                type='api'
            )
            total_cost += solution_usage['cost']
            total_tokens += solution_usage['total_tokens']
            status_updates.put({'solution': solution})
            
            # Run solution
            add_status("🔄 Running solution...", type='api')
            result = runner.run_solution(solution, request.files.get('file'))
            
            if result.get('stderr'):
                add_status(f"⚠️ Solution produced warnings/errors:\n{result['stderr']}", type='error')
            else:
                add_status("✅ Solution executed successfully", type='success')
            
            # Add final token and cost summary
            add_status(
                f"💰 Total usage - Tokens: {total_tokens}, "
                f"Total cost: ${total_cost:.4f}",
                type='api'
            )
            
            status_updates.put({'result': result.get('stdout', '')})
            status_updates.put({'message': '', 'complete': True})
            
            return render_template('components/result.html',
                                spec=spec,
                                solution=solution,
                                result=result)
            
        except Exception as e:
            error_msg = str(e)
            add_status(f"❌ Processing error: {error_msg}", True, 'error')
            status_updates.put({'message': '', 'complete': True})
            return f"Error processing request: {error_msg}", 500
            
    except Exception as e:
        error_msg = str(e)
        add_status(f"❌ Request error: {error_msg}", True, 'error')
        status_updates.put({'message': '', 'complete': True})
        return f"Error handling request: {error_msg}", 500 

@main_bp.route('/set-api-key', methods=['POST'])
def set_api_key():
    api_key = request.form.get('api_key')
    if not api_key:
        return jsonify({'error': 'No API key provided'}), 400
    
    try:
        # Validate the API key
        if llm.validate_api_key(api_key):
            Config.set_openai_key(api_key)
            return jsonify({'message': 'API key set successfully'})
        else:
            return jsonify({'error': 'Invalid API key'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500 