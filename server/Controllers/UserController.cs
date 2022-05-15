using System;
using System.Linq;
using server.Models;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace server.Controllers;

[ApiController]
public class UserController : ControllerBase
{
    [HttpPost("createuser")]
    public async Task<object> createuser([FromBody]User user)
    {
        Cryptography cryptography = new Cryptography();
        user.Password = cryptography.Encrypt(user.Password);
        await user.Save();
        return new {
            status = "OK",
            userid = user.Id
        };
    }

    [HttpPost("login")]
    public async Task<object> login([FromBody]User user)
    {
        Cryptography cryptography = new Cryptography();
        user.Password = cryptography.Encrypt(user.Password);
        var loggedusers = await Models.User.Where(u => u.Email == user.Email && u.Password == user.Password);
        var logged = loggedusers.FirstOrDefault();
        if (logged == null)
        {
            return new {
                status = "Incorrect Credentials"
            };
        }
        Token token = new Token();
        token.Moment = DateTime.Now;
        token.UserId = logged?.Id ?? "";
        await token.Save();
        
        return new {
            status = "OK",
            token = token.Id
        };
    }
}
