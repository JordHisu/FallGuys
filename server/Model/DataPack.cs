using System;
using System.Collections.Generic;

namespace server.Models;

public class DataPack : Entity<DataPack>
{
    public string Token { get; set; }
    public string? UserId { get; set; }
    public List<int>? Steps { get; set; } = new List<int>();
    public List<double>? Livelocation { get; set; } = new List<double>();
    public List<double>? Pressure { get; set; } = new List<double>();
    public DateTime? Moment { get; set; } = null;
    public override DataPack self() => this;
}