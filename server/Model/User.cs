using System.ComponentModel.DataAnnotations;
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace server.Models;
public class User : Entity<User>
{
    public string Fullname { get; set; } = "";
    public string Password { get; set; } = "";
    public string Email { get; set; } = "";
    public string Phone { get; set; } = "";
    public string? Device { get; set; } = "";
    public override User self() => this;
}