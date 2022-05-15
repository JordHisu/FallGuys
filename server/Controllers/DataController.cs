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
        var user = await TokenSystem.Test(pack.Token);
        if (user == null)
        {
            return new {
                status = "MT"
            };
        }
        for (int i = 0; i < (pack?.Steps?.Count ?? 0); i++)
        {
            await new Step()
            {
                Moment = DateTime.Now,
                UserId = user.Id,
                Value = pack.Steps[i]
            }.Save();
        }
        for (int i = 0; i < (pack?.Pressure?.Count ?? 0); i += 2)
        {
            await new Pressure()
            {
                Moment = DateTime.Now,
                UserId = user.Id,
                Low = pack.Pressure[i],
                High = pack.Pressure[i + 1]
            }.Save();
        }
        for (int i = 0; i < (pack?.Livelocation?.Count ?? 0); i += 2)
        {
            await new LiveLocation()
            {
                Moment = DateTime.Now,
                UserId = user.Id,
                Latitude = pack.Livelocation[i],
                Longitude = pack.Livelocation[i + 1]
            }.Save();
        }
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
        var pressures = await Pressure.Where(dp => dp.UserId == user.Id);
        var steps = await Step.Where(dp => dp.UserId == user.Id);
        var livelocations = await LiveLocation.Where(dp => dp.UserId == user.Id);
        
        return new {
            steps = steps.Select(x => x.Value),
            pressure = pressures.SelectMany(x => new double[] { x.Low, x.High }),
            livelocation = livelocations.SelectMany(x => new double[] { x.Latitude, x.Longitude }),
        };
    }
}