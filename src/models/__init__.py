# src/models/__init__.py
from .base_model             import Agent as BaseAgent, Env as BaseEnv
from .rd_model               import Agent as RdAgent,    Env as RdEnv
from .rd_transition_model    import Agent as RtAgent,    Env as RtEnv
from .rd_no_feebate_model    import Agent as NoFAgent,   Env as NoFEnv
from .decreasing_feebate_model import Agent as DfAgent,  Env as DfEnv

MODEL_REGISTRY = {
    "base":        (BaseAgent, BaseEnv),
    "rd":          (RdAgent,   RdEnv),
    "rd_transition": (RtAgent,   RtEnv),
    "no_feebate":  (NoFAgent,  NoFEnv),
    "decreasing_feebate": (DfAgent, DfEnv),
}

def get_model(name: str):
    try:
        return MODEL_REGISTRY[name]
    except KeyError:
        raise ValueError(f"Unknown model '{name}'. Available: {list(MODEL_REGISTRY)}")
