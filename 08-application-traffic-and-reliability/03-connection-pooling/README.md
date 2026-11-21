# Connection Pooling

## Learning Objective

Understand why applications reuse database connections instead of
creating a new connection for every request.

## 1. What Is Connection Pooling?

Connection pooling maintains a reusable collection of established
connections that an application can borrow and return.

## 2. Key Concepts

- Database connections
- Connection creation overhead
- Pool size
- Connection checkout and return
- Idle connections
- Pool exhaustion
- Connection lifetime

## 3. Typical Request Flow

1. Application requests a connection from the pool.
2. Pool provides an available connection.
3. Application executes a query.
4. Application returns the connection to the pool.

## 4. Why It Matters

Explain performance, resource usage and database connection limits.

## References

- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
