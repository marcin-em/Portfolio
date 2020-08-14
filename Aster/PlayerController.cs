using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    [SerializeField]
    bool goodLanding = false;
    public GameObject playerCrash;
    GameObject playerCrash_insta;
    public float force = 100f;
    public float rotationForce = 20f;
    [HideInInspector]public float velocity;
    public float safeVelocity;
    Rigidbody spacecraftRB;
    RaycastOne rayOne;
    RaycastTwo rayTwo;
    float defaultDrag = 0;
    float drag = 1;
    public ParticleSystem ps;
    public bool outOfFuel;
    LandingPod LP_lights;
    AudioSource audioSource;
    GameObject particleGO;

    void Start()
    {
        spacecraftRB = GetComponent<Rigidbody>();

        rayOne = GameObject.Find("Sphere1").GetComponent<RaycastOne>();
        rayTwo = GameObject.Find("Sphere2").GetComponent<RaycastTwo>();

        audioSource = gameObject.GetComponent<AudioSource>();

        spacecraftRB.useGravity = GameManager.gravity;
    }

        void Update()
    {
        if (Input.GetKeyDown(KeyCode.G))
        {
            spacecraftRB.useGravity = GameManager.gravity;
        }

        if (Input.GetKeyDown(KeyCode.Space) && GameManager.isPlayable && !outOfFuel)
        {
            audioSource.Play();
        }
        if (Input.GetKeyUp(KeyCode.Space))
        {
            audioSource.Stop();
        }
    }
    // Update is called once per frame
    void FixedUpdate()
    {
        velocity = spacecraftRB.velocity.magnitude * 10f;

        if (velocity > 200f)      //-----Maksymalna predkosc
        {
            spacecraftRB.drag = drag;
        }
        else
        {
            spacecraftRB.drag = defaultDrag;
        }

        if (Input.GetKeyDown(KeyCode.R))
        {
            Destroy(gameObject);
        }

        if (Input.GetKey(KeyCode.Space) && GameManager.isPlayable && !outOfFuel)
        {
            spacecraftRB.AddRelativeForce(Vector3.up.normalized * force);
            ps.Play();
        }
        else
        {
            ps.Stop();
        }

        if (Input.GetKey(KeyCode.LeftArrow) && GameManager.isPlayable)        
        {
            spacecraftRB.AddRelativeTorque(Vector3.forward * rotationForce);
        }
        if (Input.GetKey(KeyCode.RightArrow) && GameManager.isPlayable) 
        {
            spacecraftRB.AddRelativeTorque(-Vector3.forward * rotationForce);
        }

        if (rayOne.touchdownOne && rayTwo.touchdownTwo && goodLanding)
        {

            GameManager.isPlayable = false;
            goodLanding = false;
            LP_lights = GameObject.Find("LandingController").GetComponent<LandingPod>();
            LP_lights.touchdown = true;
            GameManager.lvlPassed = true;
        }
    }

    private void OnCollisionEnter(Collision collision)
    {
        //GROUND
        if (collision.gameObject.CompareTag("Ground") && GameManager.isPlayable)
        {
            particleGO = GameObject.Find("Particle System");
            particleGO.transform.parent = null;
            particleGO.GetComponent<DetachParticle>().crash = true;
            DestroyPlayer();
        }

        //LANDING
        if (collision.gameObject.CompareTag("Landing") && GameManager.isPlayable)
        {
            if (velocity > safeVelocity)
            {
                particleGO = GameObject.Find("Particle System");
                particleGO.transform.parent = null;
                particleGO.GetComponent<DetachParticle>().crash = true;
                DestroyPlayer();
                goodLanding = false;
            }
        }

        //ENEMY
        if (collision.gameObject.CompareTag("Enemy"))
        {
            DestroyPlayer();
        }
    }
    private void OnCollisionStay(Collision collision)
    {
        if (collision.gameObject.CompareTag("Ground"))
        {
            DestroyPlayer();
        }

        if (collision.gameObject.CompareTag("Landing") && GameManager.isPlayable && rayOne.touchdownOne && rayTwo.touchdownTwo && velocity < 40f)
        {
            goodLanding = true;
        }
        else
        {
            goodLanding = false;
        }
    }
    void DestroyPlayer()
    {
        Destroy(gameObject);
        playerCrash_insta = Instantiate(playerCrash, transform.position, transform.rotation);
        playerCrash_insta.GetComponentInChildren<Rigidbody>().velocity = spacecraftRB.velocity;
    }
}