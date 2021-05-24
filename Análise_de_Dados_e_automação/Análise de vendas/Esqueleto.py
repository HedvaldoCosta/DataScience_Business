import pandas as pd
import win32com.client as win32

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

list_email = []
n_emails = int(input('Número de emails a serem enviados: '))

for i in range(1, n_emails+1):
    email = str(input(f'Selecione o {i}º e-mail: '))
    list_email.append(email)


def get_data( path ):
    read_data = pd.read_excel( path )
    return read_data


data = get_data( 'Vendas.xlsx' )
data['ano'] = data['Data'].dt.strftime( '%y' )

faturamento = data[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()

quantidade = data[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()

ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0:'Ticket Médio'})

merge1 = pd.merge(
    left=faturamento,
    right=quantidade,
    how='inner',
    on='ID Loja'
)
merge2 = pd.merge(
    left=merge1,
    right=ticket_medio,
    how='inner',
    on='ID Loja'
)

for email in list_email:
    outlook = win32.Dispatch(dispatch='outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = f'{email}'
    mail.Subject = 'Relatório de vendas por loja'
    mail.HTMLBody = f'''
    <p>Prezados,</p>
    
    <p>Segue o relatório de vendas por loja:</p>
    
    {merge2.to_html(formatters={'Valor Final': 'R${:,.2f}'.format, 'Ticket Médio': 'R${:,.2f}'.format})}
    
    <p>Qualquer dúvida estou à disposição</p>
    <p>Hedvaldo Costa</p>
    '''
    mail.Send()
print('E-mail enviado!')
