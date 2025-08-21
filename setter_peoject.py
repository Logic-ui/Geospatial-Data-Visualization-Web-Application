class person:
    Name="Usman Ali"
    age=22
    city="Islamabada"
setattr(person,"age",23)

x=getattr(person,"age")
print(x)