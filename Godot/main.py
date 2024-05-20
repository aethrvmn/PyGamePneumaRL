from policy import policies
from agent import main
import args

for policy_name, policy in policies.items():
    main(policy_name=policy_name, policy=policy, parseargs=args.parse_args())
