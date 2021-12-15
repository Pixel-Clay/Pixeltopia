# Maps

## Tile format
```python
[biome_id, entity, resource]
```

## Map format
|**Биом**|Океан (o)|Луга (p)|Пустыня  (d)|Снег (s)|Тайга (t)|Горы (m)|
|**Цвет тайла**|`#00bfff`|`#7cfc00`|`#fce883`|`#fffafa`|`#228b22`|`#808080`|
|**id биома**|0|1|2|3|4|5|

f-лес, m-гора, p-просто земля, c-пища, a-животное, e-плодородная почва

### Пример
```csv
tm,tf,tp,tp,tp,pf,pf,pp,pf,op,op,op,op,pf,pa,pf
tf,tc,tc,tf,ta,pf,pf,pf,pp,op,op,op,op,op,pp,pc
tp,tf,tf,ta,tp,pf,pm,pp,pf,op,op,op,oa,op,op,op
tm,tc,tf,tc,tm,pf,pp,pe,pp,op,op,op,op,op,op,op
tf,tm,ta,tf,tp,pf,pe,pf,op,oa,op,op,op,op,op,op
tc,tm,tm,op,op,op,op,op,op,op,op,op,op,op,op,op
tm,tp,op,oa,op,op,op,op,op,op,sf,sa,sf,sm,op,op
ta,sp,op,op,op,op,op,op,op,sf,sa,sp,sf,sp,op,op
dp,op,op,dp,ta,da,op,op,sm,sp,sa,sc,sc,pp,op,op
dp,dc,de,dp,dc,dc,dc,dp,dp,pf,pf,pf,pf,pg,pp,pf
df,df,dc,dc,dp,dm,dm,dc,pf,pf,pp,dp,pd,dg,dc,dc
dm,df,dp,dm,op,op,dp,dp,dc,dp,dp,op,op,dp,dp,dp
op,op,op,op,op,op,op,op,op,op,op,oa,op,op,dp,da
op,op,op,op,op,op,op,op,op,op,op,op,op,op,dm,dc
op,op,op,op,op,op,op,op,op,op,dc,dp,dc,dg,da,dc
dp,dg,op,op,op,op,op,op,op,dm,dm,dg,dp,dc,dg,dc
```
