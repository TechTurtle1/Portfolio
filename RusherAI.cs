using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

/* This is a script for a basic enemy that can chase the player after the player has been in line of sight for a certain amount of time */
/* This enemy type is always watching for the player, and can use a short range attack */
public class RusherAI : MonoBehaviour
{

    /* Layer for player detection */
    [SerializeField] public LayerMask playerLayer;

    /* Layer for ground detection */
    [SerializeField] public LayerMask groundLayer;

    /* A larger enemy script */
    public EnemyScript enemy;

    /* Physics for the enemy */
    public Rigidbody2D enemyBody;

    /* The collider for the enemy */
    public BoxCollider2D box;

    /* The player object */
    public GameObject player;

    /* The player's script */
    public PlayerScript playerScript;

    /* The bar that shows the aggression of the enemy */
    public Slider aggroSlider;

    /* The range at which the enemy can 'see' the player */
    public int detectionRange;

    /* The current level of aggression. Once it reaches aggroMaxTime, enemy starts chasing the player */
    private float aggroTime;

    /* The maximum level of aggression */
    public float aggroMaxTime;

    /* The speed at which the enemy moves */
    public int speed;

    /* The height at which the player can jump */
    public int jumpHeight;

    /* The angle at which the enemy is facing */
    public float angle;

    /* The direction in which the enemy is attacking */
    public Vector2 attackDirection;

    /* The counter for when reaches 5, level of aggression decreases */
    public float deaggroTime;

    /* Since enemies have varying heights, this helps with adjusting raycast values */
    public float rusherOffset;

    // Called before the first frame update
    void Start()
    {
        enemyBody = GetComponent<Rigidbody2D>();
        enemy = GetComponent<EnemyScript>();
        box = GetComponent<BoxCollider2D>();
        player = GameObject.FindGameObjectWithTag("Player");
        playerScript = player.GetComponent<PlayerScript>();
    }

    // Runs every frame
    void Update()
    {
        /* Set the bar that shows the aggression level */
        aggroSlider.value = (float)aggroTime / aggroMaxTime;

        /* If the enemy is aggroed, moving, and otherwise has no reason to not move, then set animations to 'running' */
        enemy.top.SetBool("running", enemy.aggro && Mathf.Abs(enemyBody.velocity.x) > 0.01f && !enemy.ShouldNotMove());
        enemy.bottom.SetBool("running", enemy.aggro && Mathf.Abs(enemyBody.velocity.x) > 0.01f && !enemy.ShouldNotMove());

        /* Enemy is in docile state but is searching for the player */
        if (!enemy.aggro)
        {
            enemy.top.speed = 1;
            enemy.bottom.speed = 1;

            /* If this raycast detects the player and the player is within line of sight for a certain amount of time, then increase aggression */
            RaycastHit2D aggroer = Physics2D.Raycast((Vector2)transform.position + box.offset, Vector3.right * enemy.direction, detectionRange, playerLayer);
            if (aggroer.collider != null && (aggroer.collider.CompareTag("Player")))
            {
                /* Enemy will start chasing player */
                if (aggroTime > aggroMaxTime)
                {
                    enemy.aggro = true;
                    enemy.aggroSound.Play();
                }
                else
                {
                    aggroTime += Time.deltaTime;
                    deaggroTime = 0;
                }
            }
            else
            {
                /* If not within line of sight then count until the time to start to reduce aggression */
                if (aggroTime > 0)
                {
                    deaggroTime += Time.deltaTime;
                }
            }

            /* Player is not within line of sight for 5 seconds, decrease aggression */
            if (aggroTime > 0 && deaggroTime > 5)
            {
                aggroTime -= Time.deltaTime;
            }
            if (aggroTime < 0)
            {
                deaggroTime = 0;
            }
        }
    }

    // Runs every set quantum
    void FixedUpdate()
    {

        /* If the enemy is touching the ground, then set 'jump' animation to false */
        enemy.bottom.SetBool("jumping", !GroundCollide());

        /* Simulates how the longer an object falls, the faster it will fall. Also prevents 'floatiness' */
        if (!GroundCollide())
        {
            enemyBody.gravityScale += speed * Time.deltaTime;
        }
        else
        {
            enemyBody.gravityScale = 1;
        }

        /* If the enemy should not move or is not moving any meaningful amount, then set the x value of the enemy's velocity to zero */
        if (enemy.ShouldNotMove() || Mathf.Abs(transform.position.x - playerScript.gameObject.transform.position.x) < 0.1f)
        {
            enemyBody.velocity = new Vector3(0, enemyBody.velocity.y);
        }

        /* Enemy should not be moving while attacking or stunned */
        if (enemy.top.GetBool("attacking") || enemy.top.GetBool("stunned") || enemy.ShouldNotMove())
        {
            return;
        }

        if (enemy.aggro)
        {
            /* Calculate angle between player and enemy */
            attackDirection = (player.transform.position - transform.position).normalized;
            attackDirection.Normalize();
            angle = Mathf.Atan2(attackDirection.y, attackDirection.x) * Mathf.Rad2Deg;
            if (player.transform.position.x < transform.position.x)
            {
                angle -= 180;
            }

            /* Make enemy look at player. The 'if' statement reduces jankiness */
            if (Mathf.Abs(player.transform.position.x - transform.position.x) > 0.02f)
            {
                enemy.headPivot.transform.rotation = Quaternion.AngleAxis(angle + 90 * enemy.direction, Vector3.forward);
            }

        }


        if (enemy.aggro)
        {
            /* The faster the enemy is, the faster their running animations should be */
            enemy.top.speed = speed / 2;
            enemy.bottom.speed = speed / 2;
            aggroTime = aggroMaxTime;

            /* Orient the enemy's direction based on where the player is */
            if (player.transform.position.x > transform.position.x)
            {
                enemy.direction = 1;
            }
            else
            {
                enemy.direction = -1;
            }

            /* If the enemy is not a guard or if the enemy is a guard but is within 20 units of the object they are guarding, then continue */
            if (!enemy.isGuard || (enemy.isGuard && Vector3.Distance(transform.position, enemy.guardedObject.transform.position) < 20))
            {

                /* Player is within attacking range of the enemy and attack */
                RaycastHit2D hit = Physics2D.Raycast(transform.position, attackDirection, 1, playerLayer);
                if (hit.collider != null && hit.collider.gameObject.CompareTag("Player"))
                {
                    StartCoroutine(Attack());
                }
                else
                {
                    /* If enemy is on a steep ledge, then stop chasing the player. This is so that the player cannot just lure enemies off cliffs where they cannot return */
                    RaycastHit2D cliff = Physics2D.Raycast(new Vector2(transform.position.x + enemy.direction, transform.position.y - rusherOffset), Vector3.down, 4, groundLayer);

                    /* Enemy is not near a cliff. Chase the player */
                    if (cliff.collider != null)
                    {
                        enemyBody.velocity = new Vector2(speed * enemy.direction * enemy.miseryEnhancement, enemyBody.velocity.y);
                    }
                    else
                    {
                        enemyBody.velocity = new Vector2(0, enemyBody.velocity.y);
                    }
                }

                /* If there is a wall, then the enemy jumps over the wall */
                RaycastHit2D wallCollide = Physics2D.Raycast(new Vector2(transform.position.x, transform.position.y - rusherOffset), Vector3.right * enemy.direction, 1, groundLayer);
                if (wallCollide.collider != null && GroundCollide())
                {
                    enemyBody.velocity = new Vector2(enemyBody.velocity.x, jumpHeight);
                }
            }


        }
    }

    /* Handles a close range enemy attack */
    private IEnumerator Attack()
    {
        /* Play the attack animations, set the attack animation speed, and immobilize the enemy */
        enemy.top.SetBool("attacking", true);
        enemy.bottom.SetBool("running", false);
        enemy.top.speed = 1;
        enemy.bottom.speed = 1;
        enemyBody.velocity = new Vector2(0, enemyBody.velocity.y);

        /* This will give the player a chance to duck or dodge by waiting for two fifths of a second before dealing damage */
        yield return new WaitForSeconds(0.4f);

        /* Check if the player is within hit distance */
        RaycastHit2D hit = Physics2D.Raycast(transform.position, attackDirection, 1, playerLayer);

        /* The last check part of the 'if' statement handles an edge case where the enemy may be attacking and then stunned */
        /* Enemy should not be attacking while stunned */
        if (hit.collider != null && hit.collider.gameObject.CompareTag("Player") && !enemy.top.GetBool("stunned")
        {
            /* bloodEnhancement is an effect that increases enemy damage */
            /* Play the hit sound, decrease the player's health, interfere with what the player is doing, and create an instance of a blood splatter object */
            playerScript.ChangeHealth((int)(-enemy.damage * enemy.bloodEnhancement));
            playerScript.useProgress = 0;
            Instantiate(enemy.bloodSquib, hit.point, Quaternion.identity);
            enemy.hitSound.Play();
        }

        /* After three fifths of a second (and a second in total) return to normal behavior and deactivate the attack animation */
        yield return new WaitForSeconds(0.6f);
        enemy.top.SetBool("attacking", false);
    }

    // Checks if the enemy is touching the ground or not
    public bool GroundCollide()
    {
        return Physics2D.Raycast(box.bounds.center, Vector2.down, box.bounds.extents.y + 0.5f, groundLayer);
    }

    // Visualizes the raycasts for cliff and wall detection
    private void OnDrawGizmos()
    {
        Gizmos.DrawRay(new Vector2(transform.position.x, transform.position.y - rusherOffset), Vector3.right * enemy.direction);
        Gizmos.DrawRay(new Vector2(transform.position.x + enemy.direction, transform.position.y - rusherOffset), Vector3.down * 4);
    }
}
