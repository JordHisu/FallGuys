using System.Collections.Generic;

namespace server.Models;

public class ConfigurationPage : Entity<ConfigurationPage>
{
    public string? Token { get; set; }
    public string? UserId { get; set; }
    public double? StepSamplingRate { get; set; }
    public double? UserLocationSamplingRange { get; set; }
    public override ConfigurationPage self() => this;
}