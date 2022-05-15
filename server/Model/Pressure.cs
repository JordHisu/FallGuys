using System;

namespace server.Models;

public class Pressure : Entity<Pressure>
{
    public string? UserId { get; set; }
    public double Low { get; set; }
    public double High { get; set; }
    public DateTime? Moment { get; set; } = null;
    public override Pressure self() => this;
}