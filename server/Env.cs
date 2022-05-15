using System.IO;
using System.Linq;

public static class Env
{
    public static string Get(string variable)
        => string.Concat(
            File.ReadAllLines(".env")?
            .FirstOrDefault(ln => ln.Split('=').FirstOrDefault() == variable)?
            .SkipWhile(c => c != '=').Skip(1));
}