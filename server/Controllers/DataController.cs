using System.Linq;
using server.Models;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace server.Controllers;

[ApiController]
public class DataController : ControllerBase
{
    [HttpPost("senddata")]
    public async Task<object> senddata([FromBody]DataPack pack)
    {
        var user = await TokenSystem.Test(pack.Token);
        if (user == null)
        {
            return new {
                status = "MT"
            };
        }
        pack.UserId = user.Id;
        await pack.Save();
        return new {
            status = "OK"
        };
    }

    [HttpGet("getdata")]
    public async Task<object> getdata([FromBody]string token)
    {
        var user = await TokenSystem.Test(token);
        if (user == null)
        {
            return new {
                status = "MT"
            };
        }
        var datas = await DataPack.Where(dp => dp.UserId == user.Id);
        
        return new {
            bloodoxygen = datas.SelectMany(x => x.Bloodoxygen),
            heartbeat = datas.SelectMany(x => x.Heartbeat),
            pressure = datas.SelectMany(x => x.Pressure),
            livelocation = datas.SelectMany(x => x.Livelocation),
        };
    }
}