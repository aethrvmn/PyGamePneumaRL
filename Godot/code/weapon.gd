extends Area2D

const DAMAGE = 20
const KNOCKBACK_STR = 120

func _on_body_entered(body):
    var direction = self.global_position.direction_to(body.global_position)
    var knockback_force = direction * KNOCKBACK_STR
    if not body.is_dead:
        body.change_hp(-DAMAGE)
        body.knockback = knockback_force
        body.is_knocked = true
