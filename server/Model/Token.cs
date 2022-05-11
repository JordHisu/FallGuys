using System;

namespace server.Models;

public class Token : Entity<Token>
{
    public string UserId { get; set; }
    public DateTime Moment { get; set; }
    public override Token self() => this;
}