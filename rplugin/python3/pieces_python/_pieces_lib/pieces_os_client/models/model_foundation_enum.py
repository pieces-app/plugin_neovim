# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from pieces_python._pieces_lib.aenum import Enum, no_arg





class ModelFoundationEnum(str, Enum):
    """
    This is used to describe the foundational models used within POS.  Note: LATEST models could be used as the latests of these and then could use a system to either(check a file) or       we could add and endpoint to click out to the cloud to get the latest models and update these locally so that our users       can always have the latest without having to update the application.(not used for now)
    """

    """
    allowed enum values
    """
    GPT_3_DOT_5 = 'GPT_3.5'
    GPT_4 = 'GPT_4'
    T5 = 'T5'
    LLAMA_2_7_B = 'LLAMA_2_7B'
    LLAMA_2_13_B = 'LLAMA_2_13B'
    LLAMA_2_70_B = 'LLAMA_2_70B'
    LLAMA_3_2_B = 'LLAMA_3_2B'
    LLAMA_3_13_B = 'LLAMA_3_13B'
    LLAMA_3_70_B = 'LLAMA_3_70B'
    CODE_LLAMA_2_7_B = 'CODE_LLAMA_2_7B'
    CODE_LLAMA_2_13_B = 'CODE_LLAMA_2_13B'
    CODE_LLAMA_2_70_B = 'CODE_LLAMA_2_70B'
    BARD = 'BARD'
    ALPACA_7_B = 'ALPACA_7B'
    ALPACA_13_B = 'ALPACA_13B'
    ALPACA_33_B = 'ALPACA_33B'
    ALPACA_65_B = 'ALPACA_65B'
    VICUNA_7_B = 'VICUNA_7B'
    VICUNA_13_B = 'VICUNA_13B'
    VICUNA_33_B = 'VICUNA_33B'
    VICUNA_65_B = 'VICUNA_65B'
    GUANACO_7_B = 'GUANACO_7B'
    GUANACO_13_B = 'GUANACO_13B'
    GUANACO_33_B = 'GUANACO_33B'
    GUANACO_65_B = 'GUANACO_65B'
    OPENLLAMA_7_B = 'OPENLLAMA_7B'
    OPENLLAMA_13_B = 'OPENLLAMA_13B'
    GORILLA_7_B = 'GORILLA_7B'
    GORILLA_13_B = 'GORILLA_13B'
    GORILLA_33_B = 'GORILLA_33B'
    GORILLA_65_B = 'GORILLA_65B'
    WIZARDLM_7_B = 'WIZARDLM_7B'
    WIZARDLM_13_B = 'WIZARDLM_13B'
    WIZARDLM_30_B = 'WIZARDLM_30B'
    YULANCHAT_13_B = 'YULANCHAT_13B'
    YULANCHAT_65_B = 'YULANCHAT_65B'
    REDPAJAMA_3_B = 'REDPAJAMA_3B'
    REDPAJAMA_7_B = 'REDPAJAMA_7B'
    REDPAJAMA_13_B = 'REDPAJAMA_13B'
    REDPAJAMA_33_B = 'REDPAJAMA_33B'
    REDPAJAMA_65_B = 'REDPAJAMA_65B'
    DOLLY_70_M = 'DOLLY_70M'
    DOLLY_160_M = 'DOLLY_160M'
    DOLLY_410_M = 'DOLLY_410M'
    DOLLY_1_B = 'DOLLY_1B'
    DOLLY_1_DOT_4_B = 'DOLLY_1.4B'
    DOLLY_2_DOT_8_B = 'DOLLY_2.8B'
    DOLLY_6_DOT_9_B = 'DOLLY_6.9B'
    DOLLY_12_B = 'DOLLY_12B'
    PYTHIA_70_M = 'PYTHIA_70M'
    PYTHIA_160_M = 'PYTHIA_160M'
    PYTHIA_410_M = 'PYTHIA_410M'
    PYTHIA_1_B = 'PYTHIA_1B'
    PYTHIA_1_DOT_4_B = 'PYTHIA_1.4B'
    PYTHIA_2_DOT_8_B = 'PYTHIA_2.8B'
    PYTHIA_6_DOT_9_B = 'PYTHIA_6.9B'
    PYTHIA_12_B = 'PYTHIA_12B'
    MOSS_7_B = 'MOSS_7B'
    MOSS_13_B = 'MOSS_13B'
    RMKV_LM_100_M = 'RMKV_LM_100M'
    RMKV_LM_400_M = 'RMKV_LM_400M'
    RMKV_LM_1_DOT_5_B = 'RMKV_LM_1.5B'
    RMKV_LM_3_B = 'RMKV_LM_3B'
    RMKV_LM_7_B = 'RMKV_LM_7B'
    RMKV_LM_14_B = 'RMKV_LM_14B'
    STARCODER_15_DOT_5_B = 'STARCODER_15.5B'
    WIZARDCODER_15_B = 'WIZARDCODER_15B'
    SANTACODER_1_DOT_1_B = 'SANTACODER_1.1B'
    TEXT_BISON = 'TEXT_BISON'
    TEXTEMBEDDING_GECKO = 'TEXTEMBEDDING_GECKO'
    CHAT_BISON = 'CHAT_BISON'
    CODE_BISON = 'CODE_BISON'
    CODECHAT_BISON = 'CODECHAT_BISON'
    CODE_GECKO = 'CODE_GECKO'
    DISTILROBERTA = 'DISTILROBERTA'
    MISTRAL_7_B = 'MISTRAL_7B'
    GEMINI = 'GEMINI'
    GEMINI_1_DOT_5 = 'GEMINI_1.5'
    FAST_TEXT = 'FAST_TEXT'
    UNIXCODER = 'UNIXCODER'
    PHI_1_DOT_5 = 'PHI_1.5'
    PHI_2 = 'PHI_2'
    MIXTRAL_8_X_7_B = 'MIXTRAL_8_x_7B'
    MIXTRAL_8_X_22_B = 'MIXTRAL_8_x_22B'
    GEMMA_7_B = 'GEMMA_7B'
    GEMMA_2_B = 'GEMMA_2B'
    CODE_GEMMA_7_B = 'CODE_GEMMA_7B'
    CODE_GEMMA_2_B = 'CODE_GEMMA_2B'
    RECURRENT_GEMMA_2_B = 'RECURRENT_GEMMA_2B'
    GROK_1 = 'GROK_1'
    GROK_1_DOT_5 = 'GROK_1.5'
    CLAUDE_2 = 'CLAUDE_2'
    CLAUDE_3 = 'CLAUDE_3'
    STARLING_7_B = 'STARLING_7B'
    DBRX = 'DBRX'
    COMMAND_R_PLUS = 'COMMAND_R+'
    GEMMA_1_DOT_1_2_B = 'GEMMA_1.1_2B'
    GEMMA_1_DOT_1_7_B = 'GEMMA_1.1_7B'
    GEMMA_2_9_B = 'GEMMA_2_9B'
    PHI_3_MINI = 'PHI_3_MINI'
    PHI_3_SMALL = 'PHI_3_SMALL'
    GRANITE_3_B = 'GRANITE_3B'
    GRANITE_8_B = 'GRANITE_8B'
    LLAMA_3_8_B = 'LLAMA_3_8B'
    CLAUDE_3_DOT_5 = 'CLAUDE_3.5'
    CLAUDE_LATEST = 'CLAUDE_LATEST'
    GRANITE_LATEST = 'GRANITE_LATEST'
    LLAMA_LATEST = 'LLAMA_LATEST'
    PHI_LATEST = 'PHI_LATEST'
    GEMMA_LATEST = 'GEMMA_LATEST'
    GEMINI_LATEST = 'GEMINI_LATEST'
    GPT_LATEST = 'GPT_LATEST'
    AZURE_LATEST = 'AZURE_LATEST'
    AZURE_FAST = 'AZURE_FAST'
    AZURE_BEST = 'AZURE_BEST'
    AZURE_DEFAULT = 'AZURE_DEFAULT'
    AZURE_CUSTOM = 'AZURE_CUSTOM'
    PERPLEXITY_LATEST = 'PERPLEXITY_LATEST'
    PERPLEXITY_FAST = 'PERPLEXITY_FAST'
    PERPLEXITY_BEST = 'PERPLEXITY_BEST'
    PERPLEXITY_DEFAULT = 'PERPLEXITY_DEFAULT'
    PERPLEXITY_CUSTOM = 'PERPLEXITY_CUSTOM'

    @classmethod
    def from_json(cls, json_str: str) -> ModelFoundationEnum:
        """Create an instance of ModelFoundationEnum from a JSON string"""
        return ModelFoundationEnum(json.loads(json_str))


