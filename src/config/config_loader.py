from typing import Dict, Any
import os
from dotenv import load_dotenv
import yaml

class ConfigLoader:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Validate required environment variables
        self._validate_env_vars()
        
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI-related configuration"""
        # Load base config
        base_config = {
            'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
            'model_name': os.getenv('MODEL_NAME', 'claude-3.5-sonnet'),
            'max_tokens': int(os.getenv('MAX_TOKENS', '2000')),
            'temperature': float(os.getenv('TEMPERATURE', '0.5'))
        }
        
        # Load role guidelines
        base_config['role_guidelines'] = self._load_role_guidelines()
        
        return base_config
    
    def _validate_env_vars(self):
        """Validate that all required environment variables are present"""
        required_vars = ['ANTHROPIC_API_KEY']
        missing_vars = [key for key in required_vars if not os.getenv(key)]
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                f"Please ensure these are set in your .env file"
            )
    
    def _load_role_guidelines(self) -> Dict[str, str]:
        """Load role-specific guidelines from YAML files"""
        guidelines = {}
        prompts_dir = 'src/prompts'
        
        for filename in os.listdir(prompts_dir):
            if filename.endswith('.yaml'):
                role_name = filename.replace('.yaml', '')
                file_path = os.path.join(prompts_dir, filename)
                with open(file_path, 'r') as f:
                    config = yaml.safe_load(f)
                    if 'role_description' in config:
                        guidelines[role_name] = config['role_description']
        
        return guidelines 