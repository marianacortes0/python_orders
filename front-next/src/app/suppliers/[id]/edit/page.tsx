'use client';
import SupplierForm from '../../../../components/forms/SupplierForm';


export default function EditSupplierPage({ params }: { params: { id: string } }) {
  return <SupplierForm id={params.id} />;
}
