using System;
using MongoDB.Bson;
using System.Threading.Tasks;
using System.Linq.Expressions;
using System.Collections.Generic;
using MongoDB.Bson.Serialization.Attributes;

namespace server.Models;

public abstract class Entity<T>
    where T : Entity<T>
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }

    public async Task Save()
    {
        var access = new Access<T>();
        if (this.Id == null)
            await access.Add(self());
        else await access.Update(self());
    }
    public static async Task<IEnumerable<T>> Where(Expression<Func<T, bool>> filter)
    {
        var access = new Access<T>();
        return await access.Where(filter);
    }
    public abstract T self();
}