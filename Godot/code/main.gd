extends Node2D

@onready var main_camera = %Overworld
@onready var timer = %WorldTimer

@onready var players = $Players
#TODO: Fix camera
@onready var player_camera = $Players/Player/Camera
@onready var bamboos = $Bamboos

@onready var player_starting_pos = []
@onready var bamboo_starting_pos = []



# Called when the node enters the scene tree for the first time.
func _ready():
    main_camera.make_current()
    for player in players.get_children():
        player_starting_pos.append(player.position)
    for bamboo in bamboos.get_children():
        bamboo_starting_pos.append(bamboo.position)
    timer.start()

func _input(event):
    if event.is_action_pressed("reset_camera"):
        main_camera.make_current()
        player_camera.visible = false

func _process(delta):
    var dead_state = 0
    var i=0
    
    for bamboo in bamboos.get_children():
        if bamboo.is_dead:
            dead_state += 1
            
    if dead_state == bamboos.get_children().size():
        for player in players.get_children():
            player.change_hp(-1000)
    
func _on_player_death():
    var i = 0
    for player in players.get_children():
        player.position = player_starting_pos[i]
        player.health = 100
        player.ai_controller.done = true
        player.ai_controller.reset()
        i += 1
    var j = 0
    for bamboo in bamboos.get_children():
        bamboo.position = bamboo_starting_pos[j]
        bamboo.health = 40
        bamboo.is_dead = false
        bamboo.animation_player.play("RESET")
        j += 1

func _on_timer_timeout():
    for player in players.get_children():
        player.change_hp(-1000)
    timer.start()
    
