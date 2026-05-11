import time
import jax
import numpy as np
import jax.numpy as jnp
jax.config.update('jax_enable_x64', True) #enable double precision
#------------------------------------------------------------------------------
N   = 20480
key = jax.random.PRNGKey(0)
O   = jax.random.normal(key, [N, N], dtype=jnp.complex128)
g   = jax.random.normal(key, [N], dtype=jnp.complex128)
S   = O @ O.T.conj()
S.block_until_ready()
g.block_until_ready()
print('S.shape      :', S.shape)
print('g.shape      :', g.shape)
for k in range(4):
    print('-'*10, 'k:', k, '-'*10)
    t0  = time.time()
    x1  = jax.scipy.linalg.solve(S, g, assume_a='pos') #cholesky solver
    x1.block_until_ready()
    t1  = time.time()
    x2, *_ = jax.numpy.linalg.lstsq(S, g, rcond=None) #svd solver
    x2.block_until_ready()
    t2  = time.time()
    print('cholesky solve time  :', t1 - t0)
    print('svd solve time       :', t2 - t1)
    print('|Sx_chol-g|^2/|g|^2  :', jnp.linalg.norm(S@x1-g)**2/jnp.linalg.norm(g)**2)
    print('|Sx_svd-g|^2/|g|^2   :', jnp.linalg.norm(S@x2-g)**2/jnp.linalg.norm(g)**2)


