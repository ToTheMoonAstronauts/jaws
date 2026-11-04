# Contribution per order for proposed JAWZR tiers. Assumptions (labelled, to replace with factory quote):
VAT=0.21            # Lithuania standard VAT (B2C, prices incl. VAT)
PAY=0.029; PAYFIX=0.25   # card/PSP fee
SHIP_COST=4.50      # our cost to ship one parcel in the EU (assumption)
SHIP_FEE=4.95; FREE_FROM=49.0
COGS=[2.50,4.00,5.50]  # landed cost per 40-piece pack (assumption range)
tiers={"Basic · Hard":[(1,17.95),(3,31.95),(6,53.95)],"Premium · Ultra Hard":[(1,23.95),(3,41.95),(6,71.95)],"Current site (Hard=Ultra)":[(1,19.95),(3,34.95),(6,59.95)],"Jawliner (reference)":[(1,24.95),(3,39.95),(6,69.95)]}
print("Per-piece:")
for t,ps in tiers.items(): print(f"  {t:28s}"+"  ".join(f"{n}p €{p:.2f} (€{p/(40*n):.3f}/pc, {p/ps[0][1]:.2f}×)" for n,p in ps))
print("\nContribution per order before marketing (CAC):")
for t,ps in tiers.items():
    for n,p in ps:
        ship_in = 0 if p>=FREE_FROM else SHIP_FEE
        gross=p+ship_in; net=gross/(1+VAT); fee=gross*PAY+PAYFIX
        cells=[]
        for c in COGS:
            contrib=net-fee-SHIP_COST-c*n
            cells.append(f"COGS €{c:.2f}: €{contrib:6.2f} ({contrib/net*100:4.0f}%)")
        print(f"  {t:28s} {n} pack(s) €{p:6.2f}{' +ship' if ship_in else ' free ship'}  "+" | ".join(cells))
