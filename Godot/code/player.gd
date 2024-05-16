extends CharacterBody2D

const SPEED = 300.0

var is_attacking = false
var last_action = 0
var cooldown_start = false

var zoomed_in = false

var starting_position = self.position

signal death

@onready var ai_controller = $AIController2D

@onready var animated_sprite = $AnimatedSprite2D

@onready var overworld = %Overworld

@onready var camera = $Camera
@onready var exp_label = $Camera/ExpPanel/ExpLabel
@onready var hp_label = $Camera/HPPanel/HPLabel

@onready var attack_timer = $AttackTimer
@onready var weapon = $Weapon
@onready var weapon_player = $Weapon/AnimationPlayer


@export var health = 100
@export var experience = 0


func _ready():
    exp_label.text = "Experience\n"+str(experience)
    hp_label.text = "Health\n"+str(health)
    
func add_exp(exp_amount):
    experience += exp_amount
    ai_controller.reward = experience
    exp_label.text = "Experience\n"+str(experience)

    
func change_hp(dmg):
    health += dmg
    #ai_controller.reward += dmg/10
    if health <= 0:
        health = 0
        add_exp(-1)
        death.emit()
    hp_label.text = "Health\n"+str(health)
        
func move_left():
    last_action = 1
    velocity.x = -SPEED
func move_right():
    last_action = 3
    velocity.x = SPEED
func move_up():
    last_action = 2
    velocity.y = -SPEED
func move_down():
    last_action = 0
    velocity.y = SPEED

func _physics_process(_delta):
    velocity.x = move_toward(velocity.x, 0, SPEED)
    velocity.y = move_toward(velocity.y, 0, SPEED)
    
    # Get the input direction and handle the movement/deceleration.
    if not is_attacking:
        # Handle and movement
        ## X Axis
        if Input.is_action_pressed("move_right") or ai_controller.move == 3:
            move_right()
        if Input.is_action_pressed("move_left") or ai_controller.move == 1:
            move_left()

        ## Y Axis
        if Input.is_action_pressed("move_up") or ai_controller.move == 2:
            move_up()
        if Input.is_action_pressed("move_down") or ai_controller.move == 0:
            move_down()
        
        # Handle animations
        if velocity.x > 0:
            animated_sprite.play("move_right")
        elif velocity.x < 0:
            animated_sprite.play("move_left")
        elif velocity.y > 0 :
            animated_sprite.play("move_down")
        elif velocity.y < 0:
            animated_sprite.play("move_up")
            
        # Stop movement or change direction (left/right or up/down)
        if Input.is_action_just_released("move_right"):
            if Input.is_action_pressed("move_left"):
                move_left()
            else:
                last_action = 3
                velocity.x = move_toward(velocity.x, 0, SPEED)
                animated_sprite.play("idle_right")
        if Input.is_action_just_released("move_left"):
            if Input.is_action_pressed("move_right"):
                move_right()
            else:
                last_action = 1
                velocity.x = move_toward(velocity.x, 0, SPEED)
                animated_sprite.play("idle_left")
                
        if Input.is_action_just_released("move_up"):
            if Input.is_action_pressed("move_down"):
                move_down()
            else:
                last_action = 2
                velocity.y = move_toward(velocity.y, 0, SPEED)
                animated_sprite.play("idle_up")
        if Input.is_action_just_released("move_down"):
            if Input.is_action_pressed("move_up"):
                move_up()
            else:
                last_action = 0
                velocity.y = move_toward(velocity.y, 0, SPEED)
                animated_sprite.play("idle_down")
                
        # Handle attacking and magic
        if Input.is_action_just_pressed("attack") or ai_controller.move == 4:

            is_attacking = true
            if last_action == 1:
                weapon.position = Vector2i(-54,14)
                weapon.rotation_degrees = 90*last_action
                animated_sprite.play("attack_left")
                weapon_player.play("attack")
            elif last_action == 2:
                weapon.position = Vector2i(8,-44)
                animated_sprite.play("attack_up") 
                weapon.rotation_degrees = 90*last_action
                weapon_player.play("attack")
            elif last_action == 3:
                weapon.rotation_degrees = 90*last_action
                weapon.position = Vector2i(54,14)
                animated_sprite.play("attack_right") 
                weapon_player.play("attack")
            else:
                weapon.position = Vector2i(-12,52)
                animated_sprite.play("attack_down")
                weapon.rotation_degrees = 90*last_action
                weapon_player.play("attack")
#
        ## TODO: Fix magic
        #elif Input.is_action_just_pressed("cast_magic"):
            #is_attacking = true
            #velocity.x = move_toward(velocity.x, 0, SPEED)
            #velocity.y = move_toward(velocity.y, 0, SPEED)
            #if last_action == 1:
                #animated_sprite.play("attack_right")
            #elif last_action == 2:
                #animated_sprite.play("attack_left") 
            #elif last_action == 3:
                #animated_sprite.play("attack_up") 
            #else:
                #animated_sprite.play("attack_down")
        
        move_and_slide()
        
    else:
        attack_cooldown()        

func attack_cooldown():
    if cooldown_start == false:
        attack_timer.start()
        cooldown_start = true

# TODO: Find more elegant way to go back
func _on_button_pressed():
    if not zoomed_in:
        camera.visible = true
        camera.make_current()
        zoomed_in = true
    else:
        camera.visible = false
        overworld.make_current()
        zoomed_in = false
    

func _on_attack_timer_timeout():
    is_attacking = false
    cooldown_start = false
    weapon_player.play("RESET")
