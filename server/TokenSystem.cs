using System.Linq;
using server.Models;
using System.Threading.Tasks;

public static class TokenSystem
{
    public static async Task<User> Test(string token)
    {
        var tokens = await Token.Where(t => t.Id == token);
        if (tokens.Count() == 0)
            return null;
        var userid = tokens.FirstOrDefault()?.UserId ?? "";
        var users = await User.Where(u => u.Id == userid);
        var user = users?.FirstOrDefault();
        return user;
    }
}