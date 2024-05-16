extends CharacterBody2D

const SPEED = 150
const DAMAGE = 7
const EXP_AMOUNT = 1

@onready var knockback_timer = $KnockbackTimer
@onready var attack_timer = $AttackTimer
@onready var notice = $Notice
@onready var attack = $Attack

@onready var animation_player = $AnimationPlayer

@export var health = 100

var knockback = Vector2.ZERO
var near_player = false
var is_attacking = false
var is_knocked = false
var is_dead = false
var can_move = true

signal death


func change_hp(dmg):
    if not is_dead:
        health += dmg
        if health <= 0:
            health = 0
            for body in attack.get_overlapping_bodies():
                body.change_hp(DAMAGE)
                body.add_exp(EXP_AMOUNT)
            is_dead = true
            death.emit()

func _on_notice_body_entered(body):
    near_player = true
    body.ai_controller.reward += 1

    
func _on_notice_body_exited(body):
    near_player = false

func _on_attack_body_entered(body):
    is_attacking = false
    body.ai_controller.reward += 1

func _on_attack_body_exited(body):
    is_attacking = true

func _physics_process(delta):
    if near_player and not is_dead:
        if not is_knocked:
            for body in notice.get_overlapping_bodies():
                if self.to_local(body.global_position).x > 30:
                    velocity.x = SPEED
                elif self.to_local(body.global_position).x < -30:
                    velocity.x = -SPEED
                else:
                    velocity.x = move_toward(velocity.x, 0, SPEED)
                
                if self.to_local(body.global_position).y > 30:
                    velocity.y = SPEED
                elif self.to_local(body.global_position).y < -30:
                    velocity.y = -SPEED
                else:
                    velocity.y = move_toward(velocity.y, 0, SPEED)

                if not is_attacking:
                    for enemy in attack.get_overlapping_bodies():
                        enemy.change_hp(-DAMAGE)
                        attack_timer.start()
                    is_attacking = true
                
            
        else:
            if can_move:
                self.velocity = knockback
                knockback_timer.start()
                can_move = false
    else:
        velocity.x = move_toward(velocity.x, 0, SPEED)
        velocity.y = move_toward(velocity.y, 0, SPEED)
        
    move_and_slide()


func _on_attack_timer_timeout():
    is_attacking = false

func _on_knockback_timer_timeout():
    knockback = Vector2.ZERO
    is_knocked = false
    can_move = true
    
func _on_death():
    animation_player.play("death")
