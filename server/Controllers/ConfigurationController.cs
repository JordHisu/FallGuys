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
        if (config == null)
        {
            page.UserId = user.Id;
            await page.Save();
        }
        else
        {
            config.UserLocationSamplingRange = page.UserLocationSamplingRange ?? config.UserLocationSamplingRange;
            config.StepSamplingRate = page.StepSamplingRate ?? config.StepSamplingRate;
            config.Token = page.Token;
            await config.Save();
        }
        
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
                UserLocationSamplingRange = -1,
                StepSamplingRate = -1
            };
        }
        return new {
            status = "OK",
            StepSamplingRate = page.StepSamplingRate,
            UserLocationSamplingRange = page.UserLocationSamplingRange
        };
    }
}