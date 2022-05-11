using System.Collections.Generic;

namespace server.Models;

public class DataPack : Entity<DataPack>
{
    public string Token { get; set; }
    public string? UserId { get; set; }
    public List<double> Bloodoxygen { get; set; } = new List<double>();
    public List<double> Heartbeat { get; set; } = new List<double>();
    public List<double> Livelocation { get; set; } = new List<double>();
    public List<double> Pressure { get; set; } = new List<double>();
    public override DataPack self() => this;
}