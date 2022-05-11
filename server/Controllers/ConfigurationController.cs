using System.Linq;
using server.Models;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace server.Controllers;

[ApiController]
public class ConfigurationController : ControllerBase
{
    [HttpPost("sendconfig")]
    public async Task<object> sendconfig([FromBody]ConfigurationPage page)
    {
        var user = await TokenSystem.Test(page?.Token);
        if (user == null)
        {
            return new {
                status = "MT"
            };
        }

        var config = (await ConfigurationPage.Where(p => p.UserId == user.Id)).FirstOrDefault();
        config.Heartrange = page.Heartrange ?? config.Heartrange;
        config.Hrtbldpp = page.Hrtbldpp ?? config.Hrtbldpp;
        config.Oxygenrange = page.Oxygenrange ?? config.Oxygenrange;
        config.Userlocpp = page.Userlocpp ?? config.Userlocpp;
        config.Token = page.Token;
        config.Save();
        
        return new {
            status = "OK"
        };
    }

    [HttpGet("getconfig")]
    public async Task<object> getconfig([FromBody]string token)
    {
        var user = await TokenSystem.Test(token);
        if (user == null)
        {
            return new {
                status = "MT"
            };
        }
        var page = (await ConfigurationPage.Where(c => c.UserId == user.Id)).FirstOrDefault();
        if (page == null)
        {
            return new {
                status = "OK",
                heartrange = -1,
                hrtbldpp = -1,
                oxygenrange = -1,
                userlocpp = -1,
            };
        }
        return new {
            status = "OK",
            heartrange = page.Heartrange,
            hrtbldpp = page.Hrtbldpp,
            oxygenrange = page.Oxygenrange,
            userlocpp = page.Userlocpp,
        };
    }
}