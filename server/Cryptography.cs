
using System.Text;
using System.Globalization;
using System.Security.Cryptography;

public class Cryptography
{
    public string Encrypt(string password)
    {
        using (var hash = SHA256.Create())
        {
            var bytes = hash.ComputeHash(
            new UnicodeEncoding().GetBytes(password));

            StringBuilder hashValue = new StringBuilder(bytes.Length * 2);
            foreach (byte b in bytes)
            {
                hashValue.AppendFormat(
                CultureInfo.InvariantCulture, "{0:X2}", b);
            }
            return hashValue.ToString();
        }
    }
}