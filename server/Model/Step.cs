using System;

namespace server.Models;

public class Step : Entity<Step>
{
    public string? UserId { get; set; }
    public int Value { get; set; }
    public DateTime? Moment { get; set; } = null;
    public override Step self() => this;
}