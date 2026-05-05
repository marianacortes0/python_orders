'use client';
import { useRouter } from 'next/navigation';
import DataGrid, { Column, FilterRow, SearchPanel, Pager, Paging, Button as GridButton } from 'devextreme-react/data-grid';
import { Button } from 'devextreme-react/button';
import CustomStore from 'devextreme/data/custom_store';
import { Product } from '../../types';

const store = new CustomStore({
  key: 'id',
  load(opts) {
    const page  = Math.floor((opts.skip ?? 0) / (opts.take ?? 20)) + 1;
    const limit = opts.take ?? 20;
    const params = new URLSearchParams({ page: String(page), limit: String(limit) });
    if (opts.searchValue) params.append('search', opts.searchValue);
    return fetch(`/api/products?${params}`)
      .then(r => r.json())
      .then(d => ({ data: d.items, totalCount: d.total }));
  },
});

export default function ProductsPage() {
  const router = useRouter();
  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Productos</h1>
        <Button text="Nuevo Producto" type="default" icon="plus" onClick={() => router.push('/products/new')} />
      </div>
      <div className="card" style={{ padding: 0 }}>
        <DataGrid dataSource={store} remoteOperations={{ paging: true }} showBorders={false} showRowLines columnAutoWidth>
          <FilterRow visible />
          <SearchPanel visible placeholder="Buscar producto..." />
          <Paging defaultPageSize={20} />
          <Pager showPageSizeSelector allowedPageSizes={[10, 20, 50]} showInfo />
          <Column dataField="id"                   caption="#"         width={60} allowFiltering={false} />
          <Column dataField="productName"          caption="Producto" />
          <Column dataField="supplier.companyName" caption="Proveedor" />
          <Column dataField="unitPrice"            caption="Precio"    format={{ type: 'currency', precision: 2 }} width={110} />
          <Column dataField="package"              caption="Envase"    width={130} />
          <Column
            dataField="isDiscontinued"
            caption="Estado"
            width={130}
            cellRender={({ data }: { data: Product }) => (
              data.isDiscontinued
                ? <span className="badge badge-disc">Discontinuado</span>
                : <span className="badge badge-active">Activo</span>
            )}
          />
          <Column type="buttons" width={90}>
            <GridButton icon="eyeopen" hint="Ver"    onClick={(e: any) => router.push(`/products/${e.row.data.id}`)} />
            <GridButton icon="edit"    hint="Editar" onClick={(e: any) => router.push(`/products/${e.row.data.id}/edit`)} />
          </Column>
        </DataGrid>
      </div>
    </div>
  );
}
