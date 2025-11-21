export const metadata = {
  title: 'Slovanské Hradiská - Archív',
  description: 'Kompletný archív stránky hradiska.sk - Slovanské hradiská na Slovensku',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="sk">
      <body>{children}</body>
    </html>
  )
}
