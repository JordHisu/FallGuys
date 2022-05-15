// using FireSharp;
// using FireSharp.Config;
// using FireSharp.Interfaces;

// public class FirebaseManager
// {
//     private IFirebaseClient client;
//     private string authsecret = null;
//     private string basepath = null;

//     public FirebaseManager()
//     {
//         authsecret = Env.Get("PRIVATE_KEY_ID");
//         IFirebaseConfig config = new FirebaseConfig
//         {
//             AuthSecret = authsecret,
//             BasePath = basepath
//         };

//         client = new FirebaseClient(config);
//     }
// }