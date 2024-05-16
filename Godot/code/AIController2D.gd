extends AIController2D

# meta-name: AI Controller Logic
# meta-description: Methods that need implementing for AI controllers
# meta-default: true

#-- Methods that need implementing using the "extend script" option in Godot --#

@onready var player = $".."
@onready var bamboos = $"../../../Bamboos"
@onready var move: int

func get_obs() -> Dictionary:
    var dict = {"obs":[
    player.position.x,
    player.position.y,
    player.health,
    player.experience,
    ]}
    for bamboo in bamboos.get_children():
        dict["obs"].append(bamboo.position.x)
        dict["obs"].append(bamboo.position.y)
        dict["obs"].append(bamboo.health)
        dict["obs"].append(bamboo.position.direction_to(player.position).x)
        dict["obs"].append(bamboo.position.direction_to(player.position).y)
    return dict

func get_reward() -> float:	
    return reward
    
func get_action_space() -> Dictionary:
    return {
        "move" : {
            "size": 5,
            "action_type": "discrete"
        }
    }
    
func set_action(action) -> void:
    move = action["move"]
# -----------------------------------------------------------------------------#

#-- Methods that can be overridden if needed --#

#func get_obs_space() -> Dictionary:
# May need overriding if the obs space is complex
#	var obs = get_obs()
#	return {
#		"obs": {
#			"size": [len(obs["obs"])],
#			"space": "box"
#		},
#	}
