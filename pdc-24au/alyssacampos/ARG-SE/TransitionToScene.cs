using UnityEngine;

public class SceneController : MonoBehaviour
{
    public void OnButtonPress()
    {
        // Replace "Scene2" with your scene name
        SceneTransition.Instance.TransitionToScene("Scene2");
    }
}
