'use client';
import { useRouter } from 'next/navigation';
import DataGrid, { Column, FilterRow, SearchPanel, Pager, Paging, Button as GridButton } from 'devextreme-react/data-grid';
import { Button } from 'devextreme-react/button';
import CustomStore from 'devextreme/data/custom_store';


const store = new CustomStore({
  key: 'id',
  load(opts) {
    const page  = Math.floor((opts.skip ?? 0) / (opts.take ?? 20)) + 1;
    const limit = opts.take ?? 20;
    const params = new URLSearchParams({ page: String(page), limit: String(limit) });
    if (opts.searchValue) params.append('search', opts.searchValue);
    return fetch(`/api/customers?${params}`)
      .then(r => r.json())
      .then(d => ({ data: d.items, totalCount: d.total }));
  },
});

export default function CustomersPage() {
  const router = useRouter();
  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Clientes</h1>
        <Button text="Nuevo Cliente" type="default" icon="plus" onClick={() => router.push('/customers/new')} />
      </div>
      <div className="card" style={{ padding: 0 }}>
        <DataGrid dataSource={store} remoteOperations={{ paging: true }} showBorders={false} showRowLines columnAutoWidth>
          <FilterRow visible />
          <SearchPanel visible placeholder="Buscar..." />
          <Paging defaultPageSize={20} />
          <Pager showPageSizeSelector allowedPageSizes={[10, 20, 50]} showInfo />
          <Column dataField="id"        caption="#"        width={60} allowFiltering={false} />
          <Column dataField="firstName" caption="Nombre" />
          <Column dataField="lastName"  caption="Apellido" />
          <Column dataField="city"      caption="Ciudad" />
          <Column dataField="country"   caption="País" />
          <Column dataField="phone"     caption="Teléfono" allowFiltering={false} />
          <Column type="buttons" width={90}>
            <GridButton icon="eyeopen" hint="Ver"    onClick={(e: any) => router.push(`/customers/${e.row.data.id}`)} />
            <GridButton icon="edit"    hint="Editar" onClick={(e: any) => router.push(`/customers/${e.row.data.id}/edit`)} />
          </Column>
        </DataGrid>
      </div>
    </div>
  );
}
