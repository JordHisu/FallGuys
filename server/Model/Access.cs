using System;
using MongoDB.Driver;
using System.Threading.Tasks;
using System.Linq.Expressions;
using System.Collections.Generic;

namespace server.Models;

public class Access<T>
    where T : Entity<T>
{
    IMongoCollection<T> coll;
    public Access()
    {
        var client = new MongoClient(Env.Get("MONGOSTRING"));
        var db = client.GetDatabase("fallguys");
        this.coll = db.GetCollection<T>(typeof(T).Name);
    }

    public async Task Add(T obj)
        => await this.coll.InsertOneAsync(obj);
    
    public async Task Update(T obj)
        => await this.coll.ReplaceOneAsync(x => x.Id == obj.Id, obj);

    public async Task<IEnumerable<T>> Where(Expression<Func<T, bool>> filter)
        => await this.coll.Find(filter).ToListAsync();
}