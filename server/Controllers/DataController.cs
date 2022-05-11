using System;
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
        var tokens = await Token.Where(t => t.Id == pack.Id);
        
        if (tokens.Count() == 0)
        {
            return new {
                status = "MT"
            };
        }
        else
        {
            pack.UserId = tokens?.FirstOrDefault()?.UserId ?? "";
            await pack.Save();
            return new {
                status = "OK"
            };
        }
    }

    [HttpGet("getdata")]
    public async Task<object> getdata([FromBody]string token)
    {
        var tokens = await Token.Where(t => t.Id == token);
        if (tokens.Count() == 0)
        {
            return new {
                status = "MT"
            };
        }
        else
        {
            var userid = tokens.FirstOrDefault()?.UserId ?? "";
            var users = await Models.User.Where(u => u.Id == userid);
            var user = users?.FirstOrDefault();
            if (user == null)
            {
                return new {
                    status = "MT"
                };
            }
            var datas = await DataPack.Where(dp => dp.UserId == userid);

            return new {
                bloodoxygen = datas.SelectMany(x => x.Bloodoxygen),
                heartbeat = datas.SelectMany(x => x.Heartbeat),
                pressure = datas.SelectMany(x => x.Pressure),
                livelocation = datas.SelectMany(x => x.Livelocation),
            };
        }
    }
}