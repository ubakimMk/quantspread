# Come metterlo online (una volta sola)

1. Vai su github.com e clicca **New repository**.
2. Nome: `quantspread`. Scegli **Public**. Clicca **Create**.
3. Clicca **uploading an existing file**.
4. Trascina dentro TUTTO il contenuto della cartella (decomprimi prima lo zip).
   Importante: deve esserci anche la cartella nascosta `.github`.
   Se non la vedi, crea il file a mano: **Add file > Create new file**,
   scrivi `.github/workflows/cot.yml` e incolla il contenuto del file.
5. Clicca **Commit changes**.
6. Vai in **Settings > Pages**. In "Branch" scegli **main** e **/ (root)**. Salva.
7. Dopo 1-2 minuti il tuo sito e' online. Il link e' in alto nella pagina Pages.
8. Vai in **Settings > Actions > General**. In "Workflow permissions"
   scegli **Read and write permissions**. Salva.
9. Prova: vai in **Actions > Aggiorna CFTC > Run workflow**.
   Se diventa verde, funziona.

Da ora ogni venerdi sera l'app si aggiorna da sola.
Se per 60 giorni non succede nulla nel repository, GitHub puo fermare la pianificazione. Basta riattivarla in Actions.
