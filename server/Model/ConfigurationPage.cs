using System.Collections.Generic;

namespace server.Models;

public class ConfigurationPage : Entity<ConfigurationPage>
{
    public string? Token { get; set; }
    public string? UserId { get; set; }
    public int? Userlocpp { get; set; }
    public int? Hrtbldpp { get; set; }
    public List<int>? Heartrange { get; set; }
    public int? Oxygenrange { get; set; }
    public override ConfigurationPage self() => this;
}