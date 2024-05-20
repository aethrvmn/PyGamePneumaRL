import torch as T
import torch.nn as nn

policy_small=dict(
    net_arch=dict(
        pi=[256],
        vf=[256]
    )
)

policy_small_optim=dict(
    net_arch=dict(
        pi=[256],
        vf=[256]
    ),
    optimizer_kwargs=dict(
        betas=(0.9, 0.9),
        eps=1e-5,
    ),
)

policy_small_tanh=dict(
    activation_fn=nn.Tanh,
    net_arch=dict(
        pi=[256],
        vf=[256]
    )
)

policy_small_optim_tanh=dict(
    net_arch=dict(
        pi=[256],
        vf=[256]
    ),
    optimizer_class=T.optim.Adam,
    optimizer_kwargs=dict(
        betas=(0.9, 0.9),
        eps=1e-5,
    ),
)

policy_mid=dict(
    net_arch=dict(
        pi=[512],
        vf=[2048, 2048]
    )
)

policy_mid_tanh=dict(
    activation_fn=nn.Tanh,
    net_arch=dict(
        pi=[512],
        vf=[2048, 2048]
    )
)

policy_mid_optim=dict(
    net_arch=dict(
        pi=[512],
        vf=[2048, 2048]
    ),
    optimizer_kwargs=dict(
      betas=(0.9,0.9),
      eps=1e-5  
    )
)

policy_mid_optim_tanh=dict(
    activation_fn=nn.Tanh,
    net_arch=dict(
        pi=[512],
        vf=[2048, 2048]
    ),
    optimizer_kwargs=dict(
      betas=(0.9,0.9),
      eps=1e-5  
    )
)

policy_big=dict(
    net_arch=dict(
        pi=[1024, 1024],
        vf=[4096, 4096, 4096, 4096]
    )
)

policy_big_tanh=dict(
    activation_fn=nn.Tanh,
    net_arch=dict(
        pi=[1024, 1024],
        vf=[4096, 4096, 4096, 4096]
    )
)

policy_big_optim=dict(    
    net_arch=dict(
        pi=[1024, 1024],
        vf=[4096, 4096, 4096, 4096]
    ),
    optimizer_kwargs=dict(
        betas=(0.9, 0.9),
        eps=1e-5,
    ),
)

policy_big_optim_tanh = dict(
    activation_fn=nn.Tanh,
     net_arch=dict(
        pi=[1024, 1024],
        vf=[4096, 4096, 4096, 4096],
    ),
    optimizer_kwargs=dict(
        betas=(0.9, 0.9),
        eps=1e-5,
    ),
)

policies={
    "policy_small": policy_small,
    "policy_small_optim": policy_small_optim,
    "policy_small_tanh": policy_small_tanh,
    "policy_small_optim_tanh": policy_small_optim_tanh,
    "policy_mid": policy_mid,
    "policy_mid_optim": policy_mid_optim,
    "policy_mid_tanh": policy_mid_tanh,
    "policy_mid_optim_tanh": policy_mid_optim_tanh,       
    "policy_big": policy_big,
    "policy_big_optim": policy_big_optim,
    "policy_big_tanh": policy_big_tanh,
    "policy_big_optim_tanh": policy_big_optim_tanh,       
}
