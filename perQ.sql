SELECT i.Node as 'node', 
i.Interface as 'interface',
i.Queue as 'queue',
m.NetIntPacketsIn as 'PacketsIn',
i.NetIntPacketsOut as 'PacketsOut',
m.NetIntInTraffMeas as 'TraffIn',
i.TraffMeas as 'TraffOut',
i.NetIntErrorPacketsIn as 'ErrorsPacketsIn',
i.NetIntDropPacketsOut as 'DroppedPacketsOut'
FROM NetIntInterfaceTraffic as i JOIN NetIntInterfaceTraffic as m on (i.Node=m.Node AND i.Interface=m.Interface)
WHERE i.Queue is NOT NULL AND m.Queue is NULL
GROUP BY i.Node,i.Interface,i.Queue
