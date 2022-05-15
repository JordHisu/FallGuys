using System;

namespace server.Models;

public class LiveLocation : Entity<LiveLocation>
{
    public string? UserId { get; set; }
    public double Latitude { get; set; }
    public double Longitude { get; set; }
    public DateTime? Moment { get; set; } = null;
    public override LiveLocation self() => this;
}