using server.Models;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace server.Controllers;

[ApiController]
public class NotificationController : ControllerBase
{
    [HttpPost("sendnotif")]
    public async Task<object> sendnotif([FromBody]Notification not)
    {
        var user = await TokenSystem.Test(not.Token ?? "");
        if (user == null)
        {
            return new {
                status = "MT"
            };
        }
        not.UserId = user.Id;
        await not.Save();
        return new {
            status = "OK",
        };
    }
    
    [HttpGet("getnotif")]
    public async Task<object> getnotif([FromBody]string token)
    {
        var user = await TokenSystem.Test(token);
        if (user == null)
        {
            return new {
                status = "MT"
            };
        }
        return await Notification.Where(n => n.UserId == user.Id);
    }
}