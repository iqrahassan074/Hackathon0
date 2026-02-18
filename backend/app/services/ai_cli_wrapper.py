"""
AI CLI Wrapper
Interfaces with Claude/Qwen CLI for AI interactions
"""
import subprocess
import json
import structlog
from typing import Optional
from datetime import datetime
import os

from app.config import get_settings

logger = structlog.get_logger(__name__)


class AICLIWrapper:
    """Wrapper for interacting with AI CLI tools"""
    
    def __init__(self):
        self.settings = get_settings()
        self.timeout = self.settings.ai_cli_timeout
    
    def call_claude_cli(self, prompt: str) -> Optional[str]:
        """
        Call Claude CLI with a prompt
        
        Args:
            prompt: The prompt to send to Claude
            
        Returns:
            Response string or None if failed
        """
        try:
            # Try using claude CLI command
            # Note: Adjust command based on actual Claude CLI installation
            result = subprocess.run(
                ["claude", prompt],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode == 0:
                logger.info("claude_cli_success", prompt_length=len(prompt))
                return result.stdout
            else:
                logger.warning("claude_cli_error", error=result.stderr)
                return None
                
        except subprocess.TimeoutExpired:
            logger.warning("claude_cli_timeout", timeout=self.timeout)
            return None
        except FileNotFoundError:
            logger.warning("claude_cli_not_found", message="Claude CLI not installed")
            return None
        except Exception as e:
            logger.exception("claude_cli_exception", error=str(e))
            return None
    
    def call_qwen_cli(self, prompt: str) -> Optional[str]:
        """
        Call Qwen CLI with a prompt
        
        Args:
            prompt: The prompt to send to Qwen
            
        Returns:
            Response string or None if failed
        """
        try:
            # Try using qwen CLI command
            # Note: Adjust command based on actual Qwen CLI installation
            result = subprocess.run(
                ["qwen", prompt],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode == 0:
                logger.info("qwen_cli_success", prompt_length=len(prompt))
                return result.stdout
            else:
                logger.warning("qwen_cli_error", error=result.stderr)
                return None
                
        except subprocess.TimeoutExpired:
            logger.warning("qwen_cli_timeout", timeout=self.timeout)
            return None
        except FileNotFoundError:
            logger.warning("qwen_cli_not_found", message="Qwen CLI not installed")
            return None
        except Exception as e:
            logger.exception("qwen_cli_exception", error=str(e))
            return None
    
    def call_ai(self, prompt: str, provider: Optional[str] = None) -> Optional[str]:
        """
        Call AI CLI with automatic provider selection
        
        Args:
            prompt: The prompt to send
            provider: Optional provider override ('claude' or 'qwen')
            
        Returns:
            Response string or None if failed
        """
        if provider is None:
            provider = self.settings.ai_provider
        
        if provider == "qwen":
            return self.call_qwen_cli(prompt)
        else:
            return self.call_claude_cli(prompt)
    
    def parse_recommendations(self, response: str) -> list:
        """
        Parse AI response to extract recommendations
        
        Args:
            response: Raw AI response string
            
        Returns:
            List of recommendation strings
        """
        if not response:
            return []
        
        # Try to parse as JSON first
        try:
            data = json.loads(response)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "recommendations" in data:
                return data["recommendations"]
        except json.JSONDecodeError:
            pass
        
        # Fall back to line-by-line parsing
        lines = response.strip().split('\n')
        recommendations = []
        
        for line in lines:
            line = line.strip()
            # Remove bullet points and numbers
            if line.startswith(('-', '*', '•')):
                line = line[1:].strip()
            elif line[0].isdigit() and line[1] in '.):':
                line = line.split('.', 1)[-1].strip()
            
            if line and len(line) > 10:  # Filter out very short lines
                recommendations.append(line)
        
        return recommendations
